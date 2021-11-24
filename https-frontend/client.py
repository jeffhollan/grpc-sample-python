import grpc

# import the generated classes
from protos import greet_pb2
from protos import greet_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = greet_pb2_grpc.GreeterStub(channel)

# create a valid request message
helloRequest = greet_pb2.HelloRequest(name='Azure Container Apps')

# make the call
response = stub.SayHello(helloRequest)

# et voilà
print(response.message)