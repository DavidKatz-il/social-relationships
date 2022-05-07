
export function fileToDataUri(image) {
    return new Promise((res) => {
        const reader = new FileReader();
        reader.addEventListener('load', () => { res(reader.result); });
        reader.readAsDataURL(image);
    });
};

export async function fetchData(method, contentType, token, api, setErrorMessage, standrdErrorMessage, setData, refresher, body) {
    const requestOptions = {
        method: method,
        headers: {
            "Content-Type": contentType,
            Authorization: "Bearer " + token,
        },
        body: body,
    };
    const response = await fetch(api, requestOptions);
    var data;
    try { data = await response.json(); } catch (e) { }
    if (!response.ok) {
        if (data && data.detail) setErrorMessage(data.detail);
        else setErrorMessage(standrdErrorMessage);
        // return false;
    }
    else {
        if (setData && data) setData(data);
        if (refresher) refresher();
        //return true;
    }
}