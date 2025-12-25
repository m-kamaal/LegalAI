"""Deals with:
removing duplicates
sorting
trimming long results
preparing final payload
sample payload:

sample doc is below

{'ids': [['shaina4500_29', 'shaina4500_30']], 'embeddings': None, 'documents': [['E. VISITATION RIGHT:-', "I. That the permanent custody of minor child will remain with Petitioner/   Mother   and   Respondent Husband/   Father   of   minor   child 'AVNOOR KAUR' shall  have visitation rights   of   18   days   during   summer vacation   and   4   days   during   winter vacation in one calendar year. II. That the Respondent/Husband or his parents shall have right to meet the child on any one weekend in one month   upon   prior   intimation   to Petitioner/wife at place were petitioner/wife is residing. III. That the Respondent/Husband shall have right to make one phone call   (including   video   call)   on Mobile   No.   7579415558   per   week   to minor daughter. IV. That the child shall celebrate DIWALI   alternatively   one   year   with mother one year with father. V. That the child under no circumstances will be handed over to the custody of grand parents either"]], 'uris': None, 'included': ['metadatas', 'documents', 'distances'], 'data': None, 'metadatas': [[{'document version': '1.7.0', 'document name': 'shaina450062024_2025-09-10', 'page number': 4}, {'page number': 4, 'document name': 'shaina450062024_2025-09-10', 'document version': '1.7.0'}]], 'distances': [[0.910040020942688, 0.9938388466835022]]}

How to do all of this answered by chatgpt:
https://chatgpt.com/share/6921f9a7-dd98-800b-9368-8c9a76ee4b4c

result = {
  "ids": [[...]],
  "documents": [[doc1, doc2]],
  "metadatas": [[meta1, meta2]],
  "distances": [[dist1, dist2]]
}
"""
@staticmethod
def retreived_doc_formatter(doc):

    results = []

    docs = doc["documents"][0]
    metas = doc["metadatas"][0]
    dists = doc["distances"][0]

    for i in range(len(docs)):
        results.append({
            "document": docs[i],
            "metadata": metas[i],
            "distance": dists[i]
        })

    # sort by closest distance (smallest first)
    results.sort(key=lambda x: x["distance"])
    return results

if __name__ == "__main__":
    doc  ={'ids': [['shaina4500_29', 'shaina4500_30']], 'embeddings': None, 'documents': [['E. VISITATION RIGHT:-', "I. That the permanent custody of minor child will remain with Petitioner/   Mother   and   Respondent Husband/   Father   of   minor   child 'AVNOOR KAUR' shall  have visitation rights   of   18   days   during   summer vacation   and   4   days   during   winter vacation in one calendar year. II. That the Respondent/Husband or his parents shall have right to meet the child on any one weekend in one month   upon   prior   intimation   to Petitioner/wife at place were petitioner/wife is residing. III. That the Respondent/Husband shall have right to make one phone call   (including   video   call)   on Mobile   No.   7579415558   per   week   to minor daughter. IV. That the child shall celebrate DIWALI   alternatively   one   year   with mother one year with father. V. That the child under no circumstances will be handed over to the custody of grand parents either"]], 'uris': None, 'included': ['metadatas', 'documents', 'distances'], 'data': None, 'metadatas': [[{'document version': '1.7.0', 'document name': 'shaina450062024_2025-09-10', 'page number': 4}, {'page number': 4, 'document name': 'shaina450062024_2025-09-10', 'document version': '1.7.0'}]], 'distances': [[0.910040020942688, 0.9938388466835022]]}

    print(retreived_doc_formatter(doc))