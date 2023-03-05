from concurrent import futures
import logging

import grpc
import sound_pb2
import sound_pb2_grpc
import os
import pdb
import sys


sys.path.insert(1, '/home/jinmin645/server/model/EfficientAT')
os.chdir("./model/EfficientAT")
from model.EfficientAT.inference import inference
os.chdir("../..")


class File(sound_pb2_grpc.FileServicer):
	
    def Define(self, request, context):
        f = open('./model/EfficientAT/resources/temp.wav','wb')
        f.write(request.sound)
        f.close()
        temp=inference('./model/EfficientAT/resources/temp.wav')
        print(temp)
        #--------------------------------------------------
        keys = list(temp.keys())
        maxpercent=0.0
        result = keys[0]
        for key in keys:
            if temp[key]>maxpercent:
                result = key
                maxpercent = temp[key]
        #---------------------------------------------------
        percent = temp[result]
        if result=="Car horn":
            if percent>0.1:
                alarm=True
            else:
                alarm=False
        else:
            if percent>0.15:
                alarm=True
            else:
                alarm=False
        return sound_pb2.SoundResponse(alarm = alarm,res=result, tagging_rate=percent)

    def Connect(self, request, context):
        print(request.ping)
        return sound_pb2.Pong(pong='%s Pong!' % request.ping)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sound_pb2_grpc.add_FileServicer_to_server(File(), server)
    server.add_insecure_port('[::]:8080')
    print("server on port 8080")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()