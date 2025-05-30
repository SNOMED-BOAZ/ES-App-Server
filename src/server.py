# server.py
from concurrent import futures
import grpc
from src import synonyms_data_pb2, synonyms_data_pb2_grpc


class SynonymServiceServicer(synonyms_data_pb2_grpc.SynonymServiceServicer):
    def addSynonym(self, request, context):
        print(f"Received request at time: {request.time}")
        for synonym in request.synonyms:
            print(f"  From: {synonym.origin}, To: {synonym.new}")

        return synonyms_data_pb2.SynonymDataResponse(
            status="SUCCESS",
            message=f"Added {len(request.synonyms)} synonyms."
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    synonyms_data_pb2_grpc.add_SynonymServiceServicer_to_server(SynonymServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()