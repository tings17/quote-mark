import { useEffect, useState } from "react";
import { getAnnotations } from "../../api";
import AnnotationDetail from "./AnnotationDetail";
import { useLocation } from "react-router-dom";

function AnnotationList({ bookSpecific }) {
    const [annotations, setAnnotation] = useState([]);
    const location = useLocation();
    const bookId = bookSpecific !== undefined ? bookSpecific : location.state?.bookId;

    useEffect(() => {
        const fetchAnnotations = async() => {
            try {
                const response = await getAnnotations(bookId);
                setAnnotation(response.data);
            } catch (error) {
                console.error("Error fetching books:", error);
            }
        }
        fetchAnnotations();
    }, [bookId]);

    return (
        <div className="list">
            {
                annotations && annotations.map(annotation => {
                    return <AnnotationDetail key={annotation.id} annotation={annotation}/>
                })
            }
        </div>
    )
}

export default AnnotationList;