import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // below normal load
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 }, // normal load
    { duration: '5m', target: 200 },
    { duration: '2m', target: 300 }, // around the breaking point
    { duration: '5m', target: 300 },
    { duration: '2m', target: 400 }, // beyond the breaking point
    { duration: '5m', target: 400 },
    { duration: '10m', target: 0 }, // scale down. Recovery stage.
  ],
};

export default function () {
  const BASE_URL = 'http://host.docker.internal:5001'; // make sure this is not production

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  const body1 = JSON.stringify({
    username: 'Mateo' + Math.floor(Math.random()*10000),
    email: 'mateo'+Math.floor(Math.random()*10000)+'@gmail.com',
    password1: 'admin1',
    password2: 'admin1'
  })

  console.log(body1)

  const res = http.post(`${BASE_URL}/api/auth/signup/`, body1, params);
  check(res, {
    'is status 200': (r) => r.status === 200,
  });
}
