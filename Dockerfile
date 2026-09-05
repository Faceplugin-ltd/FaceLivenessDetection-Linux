# FaceLiveness-Linux — Linux SDK + Docker (same repo)
# Native libs are linux/amd64; image runs on any Docker host (Win/Mac/Linux).
# Before build: download Drive folder contents into ./lib/cpu/
FROM --platform=linux/amd64 python:3.12-slim-trixie

RUN apt-get update -y && apt-get install -y --no-install-recommends \
        psmisc curl util-linux e2fsprogs libgomp1 libstdc++6 libgcc-s1 libuuid1 zlib1g libssl3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/facesdk

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py sdk.py license_ux.py run.sh ./
COPY lib ./lib/

ENV LICENSE=/root/facesdk/license.txt
ENV LD_LIBRARY_PATH=/root/facesdk/lib/cpu
# Listen on product API port 8084 (same as host publish)
ENV PORT=8084
RUN chmod +x ./run.sh \
    && test -f ./lib/cpu/libFaceLivenessSDK.so \
    && test -f ./lib/cpu/libfal-eng.so \
    && test -f ./lib/cpu/fal.fpk

CMD ["./run.sh"]
EXPOSE 8084
