FROM public.ecr.aws/lambda/python:3.7

COPY requirements.txt ./
RUN pip install -U -r requirements.txt

COPY ./src ./src
RUN python ./src/train/scikit_learn_iris.py

CMD ["src/inference/app.handler"]