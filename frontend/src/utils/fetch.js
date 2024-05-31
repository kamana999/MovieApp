import axios from "axios";

/**
 * Makes an API call to the specified endpoint with the provided options.
 *
 * @param {string} ep - The endpoint to make the API call to.
 * @param {object} options - The options for the API call.
 * @param {object} options.headers - The headers to be sent with the request.
 * @param {string} options.method - The HTTP method to be used for the request.
 * @param {object} options.body - The data to be sent with the request.
 * @returns {Promise} - A promise that resolves to the response data.
 * @throws {Error} - If the API call fails.
 */
const apiCall = async (ep, options) => {
  // Construct the URL by appending the endpoint to the server URL.
  const url = `${process.env.REACT_APP_SERVER_URL}${ep}`;
  // const url = `http://localhost:5000${ep}`;

  // Destructure the options object.
  let { headers, method, body } = options;

  try {
    // Make the API call using axios.
    const response = await axios.request({
      url,
      method,
      headers,
      data: body,
    });

    // Return the response data.
    return response.data;
  } catch (error) {
    // Log the error and re-throw it.
    console.error("Error:", error);
    throw error;
  }
};

export default apiCall;
