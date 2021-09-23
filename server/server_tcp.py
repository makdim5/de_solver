import socket
import threading

from server.logic.exceptions.ExpressionMistakeException import ExpressionMistakeException
from server.logic.exceptions.ImpossibleExpressionException import ImpossibleExpressionException
from util.TimeTask import Time

from server.logic.ManagerServ import ManagerServ
from util.NumberArrayWorker import NumberArrayWorker
from util.StrArrayWorker import StrArrayWorker
from util import EXIT, SOLVE_DIFF

THREADS_AMOUNT = 5

DEFAULT_GATEWAY = "0.0.0.0"
PORT = 11000
LENGTH_QUEUE = 10
BYTES_PER_PACKAGE = 100000


def serve_client(server):
    while True:
        user_socket, address = server.accept()
        print('\nIp address and port of the client are ' + str(address) +
              "\nClient descriptor: " + str(user_socket.fileno()) +
              "\nTime of connection: " + str(Time.get_data_and_time()) +
              "\nThread: " + threading.current_thread().name + "\n")

        # получение сообщения клиенту в виде пакета в байтах
        mode = user_socket.recv(BYTES_PER_PACKAGE).decode("utf-8")

        while mode != EXIT:

            if mode == SOLVE_DIFF:
                try:
                    info = StrArrayWorker.convert_string_to_list_str(
                        user_socket.recv(BYTES_PER_PACKAGE).decode("utf-8"))

                    data = ManagerServ.solve_equation(info)

                    x_array = NumberArrayWorker.convert_list_number_to_string(data[0]).encode("utf-8")
                    user_socket.send(x_array)

                    y_array = NumberArrayWorker.convert_list_number_to_string(data[1]).encode("utf-8")

                    user_socket.send(y_array)
                except ExpressionMistakeException:
                    user_socket.send("Error: Ошибка в уравнении!!".encode("utf-8"))
                except ImpossibleExpressionException:
                    user_socket.send("Error: Невозможное выражение!!!".encode("utf-8"))
                except Exception as ex:
                    user_socket.send(("Error: " + str(ex)).encode("utf-8"))

            mode = user_socket.recv(BYTES_PER_PACKAGE).decode("utf-8")

        print(str(user_socket.fileno()) + " has entered.\n")
        user_socket.shutdown(socket.SHUT_RDWR)
        user_socket.close()


def main():
    server = socket.socket(

        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.bind(
        (DEFAULT_GATEWAY, PORT)  # localhost
    )

    threads = []

    for i in range(THREADS_AMOUNT):
        threads.append(threading.Thread(target=serve_client, args=(server,)))

    server.listen(LENGTH_QUEUE)
    print("Server is listening...\n",
          'Ip address and port of the server are ', server.getsockname(),
          " or ", socket.gethostname(),
          "\nServer descriptor: ", server.fileno())

    for item in threads:
        item.start()

    for item in threads:
        item.join()


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)
