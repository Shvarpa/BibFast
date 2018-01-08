
def citation_add_contributor(ref, citation_id, type, name):
    """add contributor to citation by its id
    :param ref:Firebase
    :param citation_id:str
    :param type:str
    :param name:str
    """
    if(name_insertion(name)==0):
        print("Error, name is not exist")
        return
    else: name=name_insertion(name)
    citation_id = str(citation_id)
    if not ref.exists('citations', citation_id):
        ref.eprint("citation #{} does'nt exist".format(citation_id))
        return
    data = ref.get('citations/{}'.format(citation_id))
    curr_citation = Citation.fromdict(data)
    report = curr_citation.add_contributor(type, name)
    if isinstance(report, str):
        ref.eprint('could not add contributor ({})'.format(report))
        return
    ref.db.child("citations/{}".format(citation_id)).set(curr_citation.data, ref.token)
    ref.eprint('add contributor to citation #{}'.format(citation_id))

def name_insertion(name):
    names=['author1','author2','author3']
    for i in range(0,len(names),1):
        if names[i].upper()==name.upper():
            return name[i]
    else: return 0


