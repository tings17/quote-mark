import { Link } from "react-router-dom";
import { logout } from "../../api";

function Navbar() {

    const handleLogout = async () => {
        try {
            await logout();
            // Force redirect to login page after logout
            window.location.href = '/login';
        } catch (error) {
            console.error("Logout failed:", error);
            // Still redirect even if there was an error
            window.location.href = '/login';
        }
    };

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/books">Book Highlighter</Link>
            </div>

            <div className="navbar-menu">
                <Link to="/books" className="navbar-item">My Library</Link>
                <Link to="/annotations/all" className="navbar-item">All Annotations</Link>
            </div>

            <div className="navbar-end">
                <button onClick={handleLogout} className="logout-button">
                    Logout
                </button>
            </div>
        </nav>
    );
}

export default Navbar;