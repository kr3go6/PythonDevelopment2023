import asyncio
import shlex
from cowsay import list_cows, cowsay

clients = {}
logged_users = {}

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())

    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                cmd_str = q.result().decode().strip()
                parsed = shlex.split(cmd_str)

                match parsed:
                    case ["who"]:
                        if me in logged_users:
                            await clients[me].put("\n>>> Users online: " + ", ".join(list(filter(lambda x: x in list_cows(),
                                    logged_users.values()))) + "\n")
                        else:
                            await clients[me].put("\n>>> You need to log in first.\n")

                    case ["cows"]:
                        await clients[me].put("\nAvailable nicknames: " + 
                                ", ".join(list(filter(lambda x: x not in logged_users.values(),
                                    list_cows()))) + "\n")

                    case ["login", username]:
                        if me in logged_users:
                            await clients[me].put("\n>>> You are already logged in.\n")
                        elif username in logged_users: 
                            await clients[me].put("\n>>> This username is already taken.\n")
                        elif username in list_cows():
                            logged_users[me] = username
                            logged_users[username] = me

                            await clients[me].put(f"\n>>> Succefully logged in as {username}.\n")
                        else:
                            await clients[me].put("\n>>> No user with such a nickname.\n" + 
                                "Enter \"cows\" to see available usernames.\n")

                    case ["say", *args]:
                        if me in logged_users:
                            if len(args) < 2:
                                await clients[me].put("\n>>> Invalid arguments\n" + 
                                        "USAGE: say username text OR say username \"text\"")
                            elif args[0] not in logged_users:
                                await clients[me].put("\n>>> This user is not online right now :(\n")
                            else:
                                await clients[logged_users[args[0]]].put(
                                        f"[{logged_users[me]} -> YOU]: \n{cowsay(' '.join(args[1:]), cow=logged_users[me])}")
                        else:
                            await clients[me].put("\n>>> You need to log in first.\n")

                    case ["yield", *args]:
                        if me in logged_users:
                            for user in logged_users.values():
                                if user not in list_cows() and user is not me:
                                    await clients[user].put(
                                            f"[{logged_users[me]} -> ALL]: \n{cowsay(' '.join(args), cow=logged_users[me])}")
                        else:
                            await clients[me].put("\n>>> You need to log in first.\n")

                    case ["quit"]:
                        send.cancel()
                        receive.cancel()
                        print(me, "DONE")

                        del clients[me]

                        if me in logged_users:
                            del logged_users[logged_users[me]]
                            del logged_users[me]

                        writer.close()
                        await writer.wait_closed()

                        return

                    case _:
                        if me not in logged_users:
                            await clients[me].put("\n>>> You need to log in first.\n")
                        else:
                            await clients[me].put("\n>>> Unknown command.\n")

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print(me, "DONE")

    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())