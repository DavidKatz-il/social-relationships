
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
            Authorization: "Bearer " + token,
            //Authorization: (token && token !== "null") ? ("Bearer " + token) : undefined,
        },
        body: body,
    };
    const response = await fetch(api, requestOptions);
    try {
        var data = await response.json();
        if (!response.ok) {
            if (data && data.detail && setErrorMessage) setErrorMessage(data.detail);
            else if (setToken) {
                setToken(null);
                if (refresher) refresher();
            }
            else if (setErrorMessage) setErrorMessage(standrdErrorMessage);
            return false;
        }
        else {
            if (setData && data) setData(data);
            if (refresher) refresher();
        }
        return true;
    } catch (e) {
        try {
            if (!response.ok) {
                if (data && data.detail && setErrorMessage) setErrorMessage(data.detail);
                else if (setToken) {
                    setToken(null);
                    if (refresher) refresher();
                }
                else if (setErrorMessage) setErrorMessage(standrdErrorMessage);
                return false;
            }
            else {
                if (setData && data) setData(data);
                if (refresher) refresher();
            }
            return true;
        }
        catch (e1) {
            console.log("faild " + e1);
            return false;
        }
        //if (setErrorMessage) setErrorMessage(standrdErrorMessage);
        if (refresher) refresher();
        return false;
    }
}