import requests
import pprint
import urllib2
from opentargets import OpenTargetsClient

STRING_API_URL = "https://string-db.org/api"

ot = OpenTargetsClient()
res = ot.search('BRAF')

def getAssociationsForDisease(disease='cancer'):
    return ot.get_associations_for_disease(disease)[0]
def getAssociationsForTarget(target="BRAF"):
    return ot.get_associations_for_target(target)
def getAssociationByID(gene, disease):
    assocs = ot.get_association('{gene}-{disease}'.format(gene=gene, disease=disease)[0])
    return assocs
#  STRING DATA
class StringData:
    def __init__(self, url):
         self.url = url
    def getStringIDs(self,lsgenes=[], limit=1):
        api_url = self.url
        output_format = "tsv-no-header"
        method = "get_string_ids"
        species = "9606"
        echo_query ="1"
        caller_identity="www.cbio.uct.ac.za"
        # build request url
        request_url = api_url + "/"+output_format + "/" + method + "?"
        request_url += "identifiers=" + "%0d".join(lsgenes)
        request_url += "&" + "species"
        request_url += "&" + "limit" + str(limit)
        request_url += "&" + "echo_query" + echo_query
        request_url += "&" + "caller_identity=" + caller_identity
        try:
            response = urllib2.urlopen(request_url)
        except Exception as e:
            print("Error occured..")
            raise
        line = response.readline()
        while line:
            l = line.split("\t")
            input_id, string_id = l[0], l[2]
            # print(input_id + "\t" + string_id + "\t"+l[4])

            line = response.readline()
    # https://string-db.org/api/[output-format]/network?identifiers=[your_identifiers]&[optional_parameters]
    def generateNetworkImage(self, lsgenes):
        api_url = self.url
        output_format = "tsv"
        method = "get_string_ids"
        species = "9606"
        add_color_nodes ="add_color_nodes"
        caller_identity="www.cbio.uct.ac.za"
        # build request url
        request_url = api_url + "/"+output_format + "/network?"
        request_url += "identifiers=" + "%0d".join(lsgenes)
        request_url += "&" + "species"
        # request_url += "&" + "add_color_nodes" + add_color_nodes
        # request_url += "&" + "echo_query" + echo_query
        request_url += "&" + "caller_identity=" + caller_identity
        try:
            response = urllib2.urlopen(request_url)
            return response
        except Exception as e:
            print("Error occured..")
            raise



def main():
    sd = StringData(STRING_API_URL)
    assocs = getAssociationsForDisease()
    my_genes = ["p53", "BRACA", "cdk2", "Q99835"]

    # pprint.pprint(assocs)

    assocs_targets = getAssociationsForTarget()

    assoc_id = getAssociationByID('ENSG00000157764', 'EFO_0005803')

    idmaps = sd.getStringIDs(my_genes)

    # print(idmaps)
    #  Network image
    network_image = sd.generateNetworkImage(my_genes)
    for obj in network_image:
        print(obj)


    # print(assoc_id)

    # for a in assocs_targets:
    #     print(a['id'], a['association_score']['overall'])
    # # for a in assocs:
    #     print(a)

if __name__ == '__main__':
    main()
