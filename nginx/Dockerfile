FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 3000

COPY clique-vpn.crt /etc/ssl/clique-vpn.crt
COPY clique-vpn.key /etc/ssl/clique-vpn.key
COPY ca.crt /etc/ssl/ca.crt

CMD ["nginx", "-g", "daemon off;"]
