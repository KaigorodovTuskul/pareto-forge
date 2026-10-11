"""Hidden, independent, deterministic I/O assertions for benchmark coding tasks.

Agent workspaces are NOT supplied this module. These are evaluation oracles, not
claims that a tiny synthetic task predicts performance on a large codebase.
"""
import hashlib
import hmac


def ex(case, expected):
    return {"input": case, "expected": expected}

TESTS = {
    'c01-normalize': [ex([' Ana ', 'ana', '', 'BOB', ' bob ', 'Éva'], ['ana','bob','éva']),ex([' A','a','B','b','C'],['a','b','c']),ex([],[]),ex(['   '],[]),ex(['Zulu','alpha','Zulu'],['zulu','alpha'])],
    'c02-count': [ex([{'type':'view'},{'type':'click'},{'type':'view'},{'type':None},{}],{'view':2,'click':1}),ex([],{}),ex([{'type':''},{'type':42},{'type':'ok'}],{'ok':1})],
    'c03-pagination': [ex({'items':[1,2,3,4,5], 'page':2,'per_page':2},{'items':[3,4],'total_pages':3,'page':2}),ex({'items':[], 'page':12,'per_page':10},{'items':[],'total_pages':0,'page':1}),ex({'items':['x'], 'page':0,'per_page':2},{'items':['x'],'total_pages':1,'page':1}),ex({'items':[1,2,3], 'page':100,'per_page':2},{'items':[3],'total_pages':2,'page':2})],
    'c04-config': [ex({'defaults':{'a':1,'b':2},'overrides':{'b':0,'c':None}},{'a':1,'b':0,'c':None}),ex({'defaults':{'flag':True},'overrides':{'flag':False}},{'flag':False}),ex({'defaults':{},'overrides':{}},{})],
    'c05-access': [ex({'role':'viewer','action':'read'}, True),ex({'role':'viewer','action':'write'},False),ex({'role':'editor','action':'delete'},False),ex({'role':'admin','action':'delete'},True),ex({'role':'owner','action':'delete'},False),ex({'role':'admin','action':'sudo'},False)],
    'c06-redact': [ex('my sk-Abc12345 and sk-ZZZZZZZZ', 'my [REDACTED] and [REDACTED]'),ex('sk-1234567 short, sk-12345678 valid','sk-1234567 short, [REDACTED] valid'),ex('no secrets','no secrets')],
    'c07-escape': [ex('<script>"a" & \'b\'</script>', '&lt;script&gt;&quot;a&quot; &amp; &#x27;b&#x27;&lt;/script&gt;'),ex('A&B','A&amp;B'),ex('', '')],
    'c08-titles': [ex([{'title':' Beta '},{'title':'Alpha'},{'title':'Alpha'},{'title':'  '},{}],['Alpha','Beta']),ex([],[]),ex([{'title':'a'}, {'title':'A'}],['A','a'])],
    'c09-retry': [ex({'status':500,'attempt':1,'max_attempts':3},True),ex({'status':429,'attempt':2,'max_attempts':2},False),ex({'status':404,'attempt':1,'max_attempts':5},False),ex({'status':503,'attempt':3,'max_attempts':4},True),ex({'status':200,'attempt':1,'max_attempts':3},False)],
    'c10-flags': [ex({'flags':{'a':False},'name':'a','default':True},False),ex({'flags':{},'name':'x','default':1},True),ex({'flags':{'a':True},'name':'a','default':False},True)],
    'c11-unique': [ex([1,2,1,3,2],[1,3,2]),ex(['x','y','x','z'],['y','x','z']),ex([],[])],
    'c12-slug': [ex(' Hello, World! ','hello-world'),ex('A___B++c','a-b-c'),ex('...',''),ex('TEST123','test123')],
    'c13-rank': [ex([{'name':'Beta','score':10},{'name':'Alpha','score':10},{'name':'Z','score':12}],['Z','Alpha','Beta']),ex([],[]),ex([{'name':'Q','score':0},{'name':'A','score':-1}],['Q','A'])],
    'c14-cart': [ex({'items':[{'price_cents':199,'quantity':2},{'price_cents':101,'quantity':1}],'discount_cents':100},399),ex({'items':[],'discount_cents':10},0),ex({'items':[{'price_cents':100,'quantity':2}],'discount_cents':999},0)],
    'c15-labels': [ex({'z':'ABC','a':'  ','b':'B'},['b','z']),ex({},[]),ex({'X':'x','a':'z'},['X','a'])],
    'c16-validate': [ex({'username':'aa','email':'bad','age':200},['username','email','age']),ex({'username':' bob ','email':'b@ex.org','age':0},[]),ex({'username':'   ','email':'x@y','age':True},['username','email','age']),ex({'username':'abc','email':'a@b.c','age':120},[])],
    'c17-dedupe': [ex([{'id':1,'v':'old'},{'id':2,'v':'a'},{'id':1,'v':'new'}],[{'id':1,'v':'new'},{'id':2,'v':'a'}]),ex([],[]),ex([{'id':'a','x':1},{'id':'a','x':2}],[{'id':'a','x':2}])],
    'c18-query': [ex('a=1&a=2&b=&x=hello+world',{'a':['1','2'],'b':[''],'x':['hello world']}),ex('',{}),ex('q=a%26b',{'q':['a&b']})],
    'c19-intervals': [ex([[1,4],[4,7],[10,12],[11,15]],[[1,7],[10,15]]),ex([[5,6],[1,2]],[[1,2],[5,6]]),ex([],[]),ex([[1,1],[1,1]],[[1,1]])],
    'c20-webhook': [],
}

def _signature(body, secret):
    return hmac.new(secret.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).hexdigest()
TESTS['c20-webhook'] = [
    ex({'body':'hello','secret':'secret','signature':_signature('hello','secret')},True),
    ex({'body':'hello!','secret':'secret','signature':_signature('hello','secret')},False),
    ex({'body':'','secret':'key','signature':_signature('','key')},True),
    ex({'body':'a','secret':'key','signature':'deadbeef'},False),
]
