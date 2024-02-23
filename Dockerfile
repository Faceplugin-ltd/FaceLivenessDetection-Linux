FROM openvino/ubuntu20_runtime:2022.3.0
RUN mkdir -p /home/openvino/faceplugin-live
WORKDIR /home/openvino/faceplugin-live
COPY ./libfacesdk1.so .
COPY ./facesdk.py .
COPY ./facebox.py .
COPY ./app.py .
COPY ./requirements.txt .
COPY ./data ./data
RUN pip3 install -r requirements.txt
CMD [ "python3", "app.py"]
EXPOSE 8080