# Node 기반 이미지 사용
FROM node:18

# 작업 디렉토리 생성
WORKDIR /app

# 나머지 프론트 코드 복사
COPY . .

# 의존성 설치
RUN npm install

# 개발 서버 실행 (개발 모드)
CMD ["npm", "start"]
