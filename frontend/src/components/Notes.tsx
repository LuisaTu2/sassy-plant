import "./Notes.css";

interface NotesProps {
  setShowNotes: React.Dispatch<React.SetStateAction<boolean>>;
}

const Notes = ({ setShowNotes }: NotesProps) => {
  return (
    <div className="notes">
      <button className="notes-close" onClick={() => setShowNotes(false)}>
        X
      </button>
      <h2>tech details & reflections</h2>
      <ul>
        <li>built on fast api, react, websockets, gpt-4o</li>
        <li>tts audio model v realtime</li>
        <li>sensors limitations</li>
      </ul>
      <h2>what's next</h2>
      <ul>
        <li>
          multiple plants, gamify with friends, plants gossip about owners
        </li>
        <li>personalized based on plant needs and "personality"</li>
        <li>create a community of plant lovers - ig for plants?</li>
        <li>listening v speaking in today's world</li>
        <li>literally touch grass</li>
      </ul>
      <h2>say hello & come get free marigold seeds :)</h2>
      <ul>
        <li>Luisa Pegoraro</li>
        <li>luisa.pegoraro@gmail.com</li>
        <li>https://findingLuisa.com</li>
        <li>QR code</li>
      </ul>
    </div>
  );
};

export default Notes;
