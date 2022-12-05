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
    const res = http.post('https://convert-api-dot-api-project-759687602744.uk.r.appspot.com/api/tasks', data, {
        headers: {
            'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NzAyMDc5ODcsImV4cCI6MTY3MDIxMTU4Nywic3ViIjoibWlndWVsIiwiaXNzIjoid3d3LnRlc3QuY29tIn0.sLWR7cEbDsYCcYTdbJ9ImGAI8zcfe-PyuUtl3mdXT2s`
        }
    });
    if(res.status != 200){
        console.log(res.body)
    }
}