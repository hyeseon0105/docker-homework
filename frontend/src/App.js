import React, { useState } from "react";
import "./App.css";

// const API_HOST = process.env.REACT_APP_API_HOST || "localhost";

function App() {
  const [counts, setCounts] = useState({ button1: 0, button2: 0 });

  // 버튼 클릭 시 해당 버튼 이름으로 POST 요청 보내기
  const handleClick = async (button) => {
    const res = await fetch(`http://54.163.43.188:5000/count/${button}`, {
      method: "POST",
    });
    const data = await res.json();

    setCounts((prev) => ({ ...prev, [button]: data.count }));
  };

  return (
    <div>
      <h1>🧮 버튼 카운터</h1>
      <button onClick={() => handleClick("button1")}>
        Button 1 클릭 수: {counts.button1}
      </button>
      <button onClick={() => handleClick("button2")}>
        Button 2 클릭 수: {counts.button2}
      </button>
    </div>
  );
}

export default App;
