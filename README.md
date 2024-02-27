<div align="center">
<img alt="" src="https://github.com/Faceplugin-ltd/FaceRecognition-Javascript/assets/160750757/657130a9-50f2-486d-b6d5-b78bcec5e6e2.png" width=200/>
</div>

# FacePlugin-FaceLivenessDetection-Docker
<div align="left">
<img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg" alt="Awesome Badge"/>
<img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/>
<img src="https://img.shields.io/github/issues/genderev/assassin" alt="issue"/>
<img src="https://img.shields.io/github/issues-pr/genderev/assassin" alt="pr"/>
</div>

<details open>
<summary><h2>Installation</h2></summary>

- build docker image
```bash
sudo docker build --pull --rm -f Dockerfile -t faceplugin-face-liveness:latest .
```

- run docker image
```bash
sudo docker run -v ./license.txt:/home/openvino/faceplugin-live/license.txt -p 8081:8080 faceplugin-face-liveness
```

</details>

<details open>
<summary><h2>Table of Contents</h2></summary>

* **[Face Detection](#face-detection)**
* **[Face Landmark Extraction](#face-landmark-extraction)**
* **[Face Liveness Detection](#face-expression-detection)**

</details>

<details open>
<summary><h2>Run Demo</h2></summary>
Please use following url or your public ip address via internet

  http://127.0.0.1:8081 or http://46.54.233.100:8081
</details>
