import json, os, sys, re

def check_global(astring):

	_a = astring.split(',')
	_ord = [sum([ord(i) for i in x if i in '}])']) for x in _a]

	return _ord.count(max(_ord))

def repair_whole(astring):

	_a = astring.split(',')
	_ord = [sum([ord(i) for i in x if i in '}])']) for x in _a]

	if '\n' in _a[_ord.index(max(_ord))]:
		rst = astring.split('\n')
		return rst

	idx = _ord.count(max(_ord))
	rst = []
	for x in range(idx):
		rst.append("".join(_a[:_ord.index(max(_ord))+1]))
		_a = _a[:_ord.index(max(_ord))]
	rst.append(_a)
	return(rst)

def clean_up(astring):

	assert type(astring) == str
	target = ('\n', ' ', '\t', '::', '://', '\\"')
	
	for t in target:
		astring = astring.replace(t, '')
	return astring


def check_json(astring):

	try:
		assert json.loads(astring)
		return True
	except Exception:
		return False


def check_quote(astring):

	a_list = astring.split(':')
	for i in range(len(a_list)):
		sub = a_list[i]
		if sub.count('"') % 2 == 1:
			print(sub)
			if sub[-1] != '"': sub += '"'
			elif '{' in sub and sub[sub.index('{')+1] != '"':
				sub = sub[:sub.index('{')+1]+'"'+sub[sub.index('{')+1:]
			elif re.findall(r'"(.*?)",(.*?)"', sub):
				sub = sub[:sub.index(',')+1]+'"'+sub[sub.index(',')+1:]
			elif re.findall(r'"(.*?),"(.*?)"', sub):
				sub = sub[:sub.index(',')]+'"'+sub[sub.index(','):]
		a_list[i] = sub
	return ":".join(a_list)


def check_token(astring):

	_astring = ("".join([x for x in astring if x in '"[]{}:(),']))
	return _astring


def repair_tocken(astring):

	astring = check_quote(astring)

	_a = astring[::-1]
	astring = astring[:-(_a.index(':'))-1]

	_astring = check_token(astring)
	try:
		assert _astring[0] + _astring[-1] == "{}"
	except AssertionError:
		if _astring[0] != "{": 
			astring = "{" + astring
			_astring = "{" + _astring
	
	memo = ''
	
	for x in _astring:
		if x == '{': memo += '}'
		elif x == '[': memo += ']'
		elif x == '(': memo += ')'
		elif x == memo[-1]: memo = memo[:-1]

	_astring = _astring[::-1]
	if _astring.index(':') > _astring.index('"'): astring += ':'
	
	astring += 'null'
	new = astring + memo[::-1]
	return new

def run(new):

	while not check_json(new):
		new = new[::-1]
		idx = min([new.index(x) for x in '{}'])
		new = new[::-1]
		new = new[:-idx-1]
		new = repair_tocken(new)
	print(new)


if __name__ == '__main__':
	
	string = open("i.json", "r")
	data = string.read()
	string.close()

	x = check_global(data)
	if x > 1:
		n = repair_whole(data)
		for new in n:
			new = clean_up(new)
			run(new)
	else:
		new = clean_up(data)
		run(new)

