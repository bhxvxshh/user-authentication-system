// NOTE: a key placed in browser JavaScript is visible to every visitor.
// Proxy this call through your backend and keep the key in an environment variable.
async function checkPNRStatus(pnr) {
    const encodedParams = new URLSearchParams();
    encodedParams.set('pnr_number', pnr);

    const options = {
        method: 'GET',
        url: 'https://indianrailways.p.rapidapi.com/findstations.php',
        params: {station: 'delhi'},
        headers: {
          'X-RapidAPI-Key': 'YOUR_RAPIDAPI_KEY',
          'X-RapidAPI-Host': 'indianrailways.p.rapidapi.com'
        }
    };

    try {
        const response = await axios.request(options);
        console.log(response.data);
        console.log("fetching done");
        return response.data;
    } catch (error) {
        console.error(error);
        return { error: 'An error occurred' };
    }
}
