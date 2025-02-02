import grpc

import passport_pb2
import passport_pb2_grpc

#############
# Constants #
#############
SEVER_ADDRESS = "localhost:50051"
PASSPORT_FILE = "passport_scan.txt"


def read_passport_number():
    with open(PASSPORT_FILE, "r") as f:
        return f.read().strip()


def run():
    print("Reading passport number from file ...")
    with grpc.insecure_channel(SEVER_ADDRESS) as channel:
        stub = passport_pb2_grpc.PassportServiceStub(channel)
        passport_number = read_passport_number()

        print(
            f"🛂 Sending passport number to competent people : {
                passport_number}"
        )
        request = passport_pb2.PassportInfosRequest(
            passportNumber=passport_number)

        try:
            response = stub.GetPassportInfos(request)
            if response.name:
                print("🎉 Passport found!\n")
                print(f"👤 Name: {response.name} {response.surname}")
                print(f"🎂 Birthdate: {response.birthDate}")
                print(f"🏠 Birthplace: {response.birthPlace}")
                print(f"📝 Status: {response.status}")
            else:
                print("🚫 Passport not found!")
        except grpc.RpcError as e:
            print(f"❌ Error: {e.details()}")


if __name__ == "__main__":
    run()
