# Edited from from https://github.com/grpc/grpc/blob/v1.41.0/examples/python/helloworld/async_greeter_server_with_graceful_shutdown.py
"""The graceful shutdown example for the asyncio Greeter server."""

import asyncio
import logging

import grpc
from protos import greet_pb2
from protos import greet_pb2_grpc

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []


class Greeter(greet_pb2_grpc.GreeterServicer):

    async def SayHello(
            self, request: greet_pb2.HelloRequest,
            context: grpc.aio.ServicerContext) -> greet_pb2.HelloReply:
        logging.info('Received gRPC request')
        return greet_pb2.HelloReply(message='Hello, %s!' % request.name)


async def serve() -> None:
    server = grpc.aio.server()
    greet_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()

    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()