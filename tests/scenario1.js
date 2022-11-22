import http from 'k6/http';
import {
    oauth
} from './oauth.js';

export const options = {
    vus: 5, // Virtual Users
    duration: '1m',
}

export function setup() {
    return '23'
}

const files = [
    'audio5.ogg',
    'audio23.ogg',
    'audio24.ogg',
    'audio25.ogg',
    'audio26.ogg'
]
const dir = {}
files.forEach(elem => {
    dir[elem] = open(`/scripts/audios/${elem}`, 'b')
})
export default function (token) {
    const randomName = files[Math.floor(Math.random() * files.length)];
    const data = {
        newFormat: 'mp3',
        fileName: http.file(dir[randomName], randomName)
    };
    const res = http.post('http://35.245.192.250:5001/api/tasks', data, {
        headers: {
            'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NjkwOTcxNDYsImV4cCI6MTY2OTEwMDc0Niwic3ViIjoiaXNtYWVsMiIsImlzcyI6Ind3dy50ZXN0LmNvbSJ9.tE5mz9x_lp9R9WsVLVIkI_Cj57ryu_WhC58xzk1OO3A`
        }
    });
    if(res.status != 200){
        console.log(res.body)
    }
}