async function checkPNRStatus(pnr) {
    const encodedParams = new URLSearchParams();
    encodedParams.set('pnr_number', pnr);

    const options = {
        method: 'GET',
        url: 'https://indianrailways.p.rapidapi.com/findstations.php',
        params: {station: 'delhi'},
        headers: {
          'X-RapidAPI-Key': '90fa6b1258msh589cc75fb310f65p146d0ajsnf3f0c4a52f6f',
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
