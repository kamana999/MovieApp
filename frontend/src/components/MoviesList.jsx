import React, { useEffect, useState } from "react";
import { Table, Pagination } from "react-bootstrap";
import apiCall from "../utils/fetch";

// class MovieList extends React.Component {
const MovieList = () => {
  const [movieList, setMovieList] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(100);
  const [movieCount, setMovieCount] = useState(0);

  const loadMoviesList = async () => {
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    };
    let data = await apiCall(
      `/api/movies/list/?page=${currentPage}&page_size=${itemsPerPage}`,
      options
    );
    if (data.data) {
      setMovieList(data.data);
      setMovieCount(data.total_count);
    }
  };

  useEffect(() => {
    loadMoviesList();
  }, [currentPage]);
  useState(() => {
    loadMoviesList();
  }, [movieList]);

  return (
    <>
      <h1 style={{ textAlign: "center", marginTop: "2%" }}>Movie List</h1>
      <Pagination
        style={{ display: "flex", justifyContent: "center", marginTop: "2%" }}
      >
        {Array.from(
          { length: Math.ceil(movieCount / itemsPerPage) },
          (_, index) => (
            <Pagination.Item
              key={index}
              active={index + 1 === currentPage}
              onClick={() => setCurrentPage(index + 1)}
            >
              {index + 1}
            </Pagination.Item>
          )
        )}
      </Pagination>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Show ID</th>
            <th>Type</th>
            <th>Title</th>
            <th>Director</th>
            <th>Cast</th>
            <th>Country</th>
            <th>Date Added</th>
            <th>Release Year</th>
            <th>Rating</th>
            <th>Duration</th>
            <th>Listed In</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {movieList.map((item, index) => (
            <tr key={index}>
              <td>{item.show_id}</td>
              <td>{item.type}</td>
              <td>{item.title}</td>
              <td>{item.director}</td>
              <td>{item.cast}</td>
              <td>{item.country || "N/A"}</td>
              <td>{item.date_added}</td>
              <td>{item.release_year}</td>
              <td>{item.rating}</td>
              <td>{item.duration}</td>
              <td>{item.listed_in}</td>
              <td>{item.description}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </>
  );
};

export default MovieList;
