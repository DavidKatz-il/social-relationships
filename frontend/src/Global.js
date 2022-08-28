
export function fileToDataUri(image) {
    return new Promise((res) => {
        const reader = new FileReader();
        reader.addEventListener('load', () => { res(reader.result); });
        reader.readAsDataURL(image);
    });
};

export async function fetchData(method, contentType, token, api, setErrorMessage, standrdErrorMessage, setData, refresher, body, setToken) {
    const requestOptions = {
        method: method,
        headers: {
            "Content-Type": contentType,
            Authorization: (token && token !== "null") ? ("Bearer " + token) : undefined,
        },
        body: body,
    };
    const response = await fetch(api, requestOptions);
    var data;
    try {
        data = await response.json();
        if (!response.ok) {
            if (data && data.detail && setErrorMessage) setErrorMessage(data.detail);
            else if (setToken) {
                setToken(null);
                if (refresher) refresher();
            }
            else setErrorMessage(standrdErrorMessage);
        }
        else {
            if (setData && data) setData(data);
            if (refresher) refresher();
        }
    } catch (e) { }
}