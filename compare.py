import dns.resolver

root = 'example.com'
subs = ['www','dev']
name_server1 = ['8.8.8.8']
name_server2 = ['another.nameserver.com']
verbose = False


matches = set()
mismatches = set()
def get_result(resolver, domain, record_type):
	try:
		return resolver.query(domain,record_type,dns.rdataclass.IN, False, None, False)
	except :
		return []

def print_result(ans) :
	try :
		for data in ans:
			print (data)
	except TypeError :
		print('NO')

def make_items(ans):
	results = dict()
	try :
		for data in ans:
			split = str(data).split()
			if len(split) == 2 :
				results[split[1].lower()] = {'priority' : split[0]}
			else :
				results[str(data).lower()] = {}
		return results
	except TypeError :
		return results

def compare(resolver1, resolver2, domain, record_type):
	r1 = make_items(get_result(resolver1, domain,record_type))
	r2 = make_items(get_result(resolver2, domain,record_type))
	allresulsts = set(list(r1.keys())+list(r2.keys()))
	if len(allresulsts)==0 :
		return
	print (">>>> COMPARE : " + domain + " " + record_type)
	mismatch_found = False
	if verbose :
		print('1 : ' + str(r1))
		print('2 : ' + str(r2))
	for h in allresulsts :
		if h in r1 and h in r2 :
			print("\tmatch! " + h)
			
		else :
			mismatch_found = True
			if verbose == False :
				print('1 : ' + str(r1))
				print('2 : ' + str(r2))
			print("\tmismatch! " + h)

	if mismatch_found == False :
		matches.add(record_type+'@'+domain)
	else :
		mismatches.add(record_type+'@'+domain)

	print("")

fR = dns.resolver.Resolver(configure=False)
sR = dns.resolver.Resolver(configure=False)
fR.nameservers = [ item.address for server in name_server1 for item in dns.resolver.query(server) ]
sR.nameservers = [ item.address for server in name_server2 for item in dns.resolver.query(server) ]

root_TYPES = ['MX', 'TXT', 'A', 'CNAME']
SUB_TYPES = ['A', 'CNAME']
for t in root_TYPES :
	compare(fR, sR, root, t)
for sub in subs :
	for t in SUB_TYPES :
		compare(fR, sR, sub + '.' +root, t)
matches = sorted(list(matches))
mismatches = sorted(list(mismatches))
print(">>Results<<")
print(">>Matched")
for h in matches:
	print('\t'+h)
print(">>Mismatched")
for h in mismatches:
	print('\t'+h)
