import json
from concurrent import futures

import grpc

import passport_pb2
import passport_pb2_grpc

#############
# Constants #
#############
DATABASE_PATH = "./passport_db.json"


def load_db():
    with open(DATABASE_PATH, "r") as database_file:
        return json.load(database_file)


class PassportService(passport_pb2_grpc.PassportServiceServicer):
    def GetPassportInfos(self, request, context):
        database = load_db()
        passport_number = request.passportNumber

        if passport_number in database:
            passport_data = database[passport_number]
            return passport_pb2.PassportInfos(
                passportNumber=passport_number,
                name=passport_data["name"],
                surname=passport_data["surname"],
                birthDate=passport_data["birthDate"],
                birthPlace=passport_data["birthPlace"],
                status=passport_data["status"]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Passport number {passport_number} not found")
            return passport_pb2.PassportInfos()


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    passport_pb2_grpc.add_PassportServiceServicer_to_server(
        PassportService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
