import "./Notes.css";
import LiLogo from "../assets/li-qr-code.jpeg";

interface NotesProps {
  setShowNotes: React.Dispatch<React.SetStateAction<boolean>>;
}

const Notes = ({ setShowNotes }: NotesProps) => {
  return (
    <div className="notes">
      <div className="notes-btn-wrapper">
        <button className="notes-btn" onClick={() => setShowNotes(false)}>
          X
        </button>
      </div>
      <h2>tech details & reflections</h2>
      <ul>
        <li>
          built on fast api, react, websockets & http, <strong>gpt-4o</strong>
        </li>
        <li>tts audio model v realtime</li>
        <li>sensors limitations</li>
      </ul>
      <h2>what's next</h2>
      <ul>
        <li>
          multiple plants, <strong>gamify</strong> with friends, plants gossip
          about owners
        </li>
        <li>
          personalized based on plant needs and "personality",{" "}
          <strong>train llm</strong>
        </li>
        <li>
          create a <strong>community</strong> of plant lovers
        </li>
        <li>listen to the world around us</li>
        <li>go touch grass 😊 ⋆.ೃ࿔* :･🌱⋆.ೃ࿔* :･</li>
      </ul>
      <h2>say hello & come get free marigold seeds :)</h2>{" "}
      <ul>
        <li>Luisa Pegoraro</li>
        <li>email: luisa.pegoraro@gmail.com</li>
        <li>portfolio: https://findingLuisa.com</li>
      </ul>
      <div className="linked-qr-code-wrapper">
        <div className="linkedin-connect"> Let's connect on LinkedIn!</div>
        <img src={LiLogo} alt="linkedin-qr-code" className="linkedin-qr-code" />
      </div>
    </div>
  );
};

export default Notes;
