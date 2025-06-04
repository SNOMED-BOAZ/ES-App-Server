# server.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import grpc
from concurrent import futures
from src import synonyms_data_pb2, synonyms_data_pb2_grpc
from collections import defaultdict

class SynonymServiceServicer(synonyms_data_pb2_grpc.SynonymServiceServicer):
    def addSynonym(self, request, context):
        print(f"Received request at time: {request.time}")

        synonyms_file = os.path.join(os.path.dirname(__file__), "../elasticsearch/elk/elasticsearch/config/synonyms.txt")

        try:
            # 파일을 읽어 기존 동의어 맵 구성: target => [origin1, origin2, ...]
            synonym_map = defaultdict(set)
            if os.path.exists(synonyms_file):
                with open(synonyms_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if "=>" in line:
                            left, right = line.split("=>")
                            origins = [term.strip() for term in left.split(",")]
                            target = right.strip()
                            for term in origins:
                                synonym_map[target].add(term)

            # 새 요청 반영
            for synonym in request.synonyms:
                origin = synonym.origin.strip()
                new = synonym.new.strip()
                print(f"From: {origin}, To: {new}")
                synonym_map[new].add(origin)

            # 파일 다시 쓰기
            with open(synonyms_file, "w", encoding="utf-8") as f:
                for target, origins in synonym_map.items():
                    origin_list = sorted(origins)
                    f.write(f"{','.join(origin_list)} => {target}\n")

            return synonyms_data_pb2.SynonymDataResponse(
                status="SUCCESS",
                message=f"Updated synonyms.txt with {len(request.synonyms)} synonyms."
            )

        except Exception as e:
            print(f"[ERROR] Failed to update file: {e}")
            return synonyms_data_pb2.SynonymDataResponse(
                status="FAILURE",
                message=f"Error: {str(e)}"
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