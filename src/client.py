# client.py
import grpc
from src import synonyms_data_pb2, synonyms_data_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = synonyms_data_pb2_grpc.SynonymServiceStub(channel)

    synonym_list = [
        synonyms_data_pb2.Synonym(origin="car", new="automobile"),
        synonyms_data_pb2.Synonym(origin="bike", new="bicycle")
    ]

    request = synonyms_data_pb2.SynonymDataRequest(
        time="2025-05-30T19:00:00Z",
        synonyms=synonym_list
    )

    response = stub.addSynonym(request)
    print("Status:", response.status)
    print("Message:", response.message)

if __name__ == '__main__':
    run()