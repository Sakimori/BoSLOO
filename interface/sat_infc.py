import asyncio, telnetlib3

@asyncio.coroutine
def shell(reader, writer):
    writer.write('\r\nWelcome to the BoSLOO Primitive Interface!\r\nBPI for debugging and has no checking or feedback, use with caution!\r\n-=>')
    go = True
    com = ""
    while go:
        inp = yield from reader.read(1)
        for c in inp:
            com += c
            if c == '\x7f':
                writer.write("\r" + " "*(len(com)+1))
                com = com[:-2]
                writer.write("\r-=>" + com + " ")
                writer.write("\r-=>" + com)
                yield from writer.drain()
            else:
                writer.echo(inp)
            if c == '\r':
                print(com)
                writer.write('\r\n')
                com = com.strip()
                if com == "bye":
                    writer.close()
                    go = False
                elif com[:4] == "help":
                    writer.write('ops: GET/SET/EXE\r\n')
                    writer.write('Op:MTE(s):Subsystem:Field:Parameter\r\n')
                    writer.write('Parameter only for SET\r\n')
                    writer.write('MTE to get current time\r\n')
                    yield from writer.drain()
                elif com[:4].upper() == "GET:" or com[:4].upper() == "SET:" or com[:4].upper() == "EXE:":
                    parts = com.split(":")
                    if (parts[0].upper() == "GET" or parts[0].upper() == "EXE") and len(parts) == 4:
                        print("wrote command = ", parts[1]+":"+parts[0].upper()+":"+parts[2]+":"+parts[3])
                        with open('../satsim/command_q', "a") as q:
                            q.write(parts[1]+":"+parts[0].upper()+":"+parts[2]+":"+parts[3]+"\n")
                    elif parts[0].upper() == "SET" and len(parts) == 5:
                        print("wrote command = ", parts[1]+":"+parts[0].upper()+":"+parts[2]+":"+parts[3]+":"+parts[4])
                        with open('../satsim/command_q', "a") as q:
                            q.write(parts[1]+":"+parts[0].upper()+":"+parts[2]+":"+parts[3]+":"+parts[4]+"\n")
                    else:
                        writer.write("BAD OP COMMAND\r\n")
                        yield from writer.drain()
                elif com[:3].upper() == "MTE" and len(com) == 3:
                    with open("../satsim/status", "r") as statfile:
                        mte = statfile.read()
                    writer.write(mte + "\r\n")
                    yield from writer.drain()
                else:
                        writer.write("BAD COMMAND\r\n")
                        yield from writer.drain()
                if go:
                    writer.write('-=>')
                    yield from writer.drain()
                    com = ""

loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=7000, shell=shell)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())