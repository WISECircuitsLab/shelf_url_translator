console.log("Hello, World!");

const parameter_name = "wise_id";
const column_name = "WISE_ID";
const qr_id_column_name = "Shelf_QR_ID";
const url_prefix = "https://eam.sh/";

var data = null;

// Function to get the query parameter value of parameter_name from the URL
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

function parseCSV(data) {
    const lines = data.split('\n');
    const headers = lines[0].split(',');
    // Clean up headers by trimming whitespace
    for (let i = 0; i < headers.length; i++) {
        headers[i] = headers[i].trim();
    }
    const rows = lines.slice(1).map(line => {
        const values = line.split(',');
        const row = {};
        headers.forEach((header, index) => {
            row[header] = values[index];
        });
        return row;
    });

    return rows;
}

(async () => {
    try {
        //read .csv file on a server
        const target = `https://docs.google.com/spreadsheets/d/e/2PACX-1vQLl77CDbnnQONiL4kM051ftURDtCISZKys8HPrdeF9t_MgOiggWcMkC6Y8pWb1ZM6AlQj_C4ygTAgo/pub?gid=0&single=true&output=csv`;

        const res = await fetch(target, {
            method: 'get',
            headers: {
                'content-type': 'text/csv;charset=UTF-8',
            }
        });

        if (res.status === 200) {
            data = await res.text();
            console.log(data);
            findRowByQueryParam();

        } else {
            console.log(`Error code ${res.status}`);
        }
    } catch (err) {
        console.log(err);
    }
})();


// Function that parses CSV data into an array of objects
// Get the value of the query parameter
// Search for the row where column_name matches the query parameter value
// Print the matching row to the console
function findRowByQueryParam() {
    const queryValue = getQueryParam(parameter_name);
    console.log(`Searching for ${column_name} = ${queryValue}`);
    const rows = parseCSV(data);
    const matchingRow = rows.find(row => row[column_name] === queryValue);
    console.log(matchingRow);
    const qrId = matchingRow ? matchingRow[qr_id_column_name] : null;
    console.log(`Found ${qr_id_column_name}: ${qrId}`);
    const finalUrl = qrId ? url_prefix + qrId : null;
    console.log(`Final URL: ${finalUrl}`);
    if (finalUrl) {
        window.location.href = finalUrl;
    }

}
