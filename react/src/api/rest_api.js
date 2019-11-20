import axios from 'axios';
import { toast } from 'react-toastify';

let browserCurrentUrl = window.location.href;
let apiUrl = "production url"

// dev mode
if (browserCurrentUrl.indexOf("http://localhost") >= 0) {
    apiUrl = "http://localhost:5000"
}

export let url = apiUrl;

// axios
let api = axios.create({
    baseURL: url
});

// get 
export const getData = async () => {
    try {
        const response = await api.get(`${url}/api/data/getall`, { withCredentials: true });
        return response.data;
    }
    catch (error) {
        console.log(error);
    }

    return null;
}

// POST

export const postNewData = (body1, body2, callback) => {

    api.post(`${url}/api/data/postdata`, {
        body1: body1,
        body2: body2
    }, { withCredentials: true })
        .then((response) => {
            // console.log(response);
            toast.success("successfuly")
            callback();
        }, (error) => {
            console.log(error);
        });

}

export default api;