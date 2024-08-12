FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 3000

COPY ontopvpn.crt /etc/ssl/ontopvpn.crt
COPY ontopvpn.key /etc/ssl/ontopvpn.key

CMD ["nginx", "-g", "daemon off;"]
