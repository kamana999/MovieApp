import React, { useEffect, useState } from "react";
import { Table, Pagination, Container} from "react-bootstrap";
import { BsSortDown, BsSortUp } from "react-icons/bs";
import apiCall from "../utils/fetch";

// class MovieList extends React.Component {
const MovieList = () => {
  const [movieList, setMovieList] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(30);
  const [order, setOrder] = useState(1);
  const [column, setColumn] = useState("_id");

  const loadMoviesList = async () => {
    const options = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    };
    let data = await apiCall(
      `/api/movies/list/?page=${currentPage}&page_size=${itemsPerPage}&sort_key=${column}&sort_value=${order}`,
      options
    );
    if (data.data) {
      setMovieList(data.data);
    }
  };

  const handleSortIconHandler  = (column_name) => {  
    return(
      <span style={column !== column_name ? { color: "gray" } : {color: "black", fontWeight: "bold"}}> {
        order === 1 || column !== column_name ? (
          <BsSortDown onClick={() => handleSort(column_name)} />
        ) : (
          <BsSortUp onClick={() => handleSort(column_name)} />
        )
      }</span>
    )
  }

  const handleSort = (column_name) => {
    if (column_name === column) {
      setOrder(order * -1);
    } else {
      setColumn(column_name);
      setOrder(1);
    }
    loadMoviesList();
  };

  useEffect(() => {
    loadMoviesList();
  }, [currentPage]);



  return (
    <>
      <h1 style={{ textAlign: "center", marginTop: "2%" }}>Movie List</h1>
      
      <Container style={{ marginTop: "2%" }}>
        <Pagination>
          <Pagination.Prev
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
          />
          <Pagination.Item>{currentPage}</Pagination.Item>
          <Pagination.Next
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={movieList.length !== itemsPerPage}
          />
        </Pagination>
      </Container>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>
              Show ID
              {handleSortIconHandler("show_id")}

            </th>
            <th>Type</th>
            <th>Title</th>
            <th>Director</th>
            <th>Cast</th>
            <th>Country</th>
            <th>Date Added {handleSortIconHandler("date_added")}</th>
            <th>Release Year {handleSortIconHandler("release_year")}</th>
            <th>Rating</th>
            <th>Duration {handleSortIconHandler("release_year")}</th>
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
              <td>
                {new Date(item.date_added).toLocaleDateString("en-US", {
                  month: "long",
                  day: "numeric",
                  year: "numeric",
                }) || "N/A"}
              </td>
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
