FROM openvino/ubuntu20_runtime:2022.3.0
RUN mkdir -p /home/openvino/faceplugin-live
WORKDIR /home/openvino/faceplugin-live
COPY ./faceplugin.so .
COPY ./facesdk.py .
COPY face_util.py .
COPY ./app.py .
COPY ./requirements.txt .
COPY ./data ./data
RUN pip3 install -r requirements.txt

EXPOSE 8888

ENTRYPOINT ["python3"]
CMD ["app.py"]