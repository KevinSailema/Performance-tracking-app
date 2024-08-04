import { isValidElement } from "react";
import { useState } from "react";
import ImagenPRofesor from "../assets/profesor.jpg";
import Button from "react-bootstrap/Button";

import 'bootstrap/dist/css/bootstrap.min.css';
import "../styles/components/Tabs.css"


type TabsProps = {
    children: React.ReactNode[];
}

function Tabs({ children }: TabsProps) {

    const [tabActivo, setTabActivo] = useState<string>(
        isValidElement(children[0])
            ?
            children[0].props.id
            :
            ""
    );

    const cambiarTab = (e: React.MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        if (e.target instanceof HTMLAnchorElement) {
            setTabActivo(e.target.innerText);
        }
    }

    return (
        <div className="contenedor-tabs">
            <nav className="barra-lateral">
                <div className="perfil-profesor">
                    <img src={ImagenPRofesor} alt="Foto de perfil del profesor de la asignatura" />
                    <p>Mario Romero</p>
                </div>
                <div className="tabs">
                    {
                        children.map((tab) => {
                            if (isValidElement(tab)) {
                                return (
                                    <a
                                        className={"tab " + (tabActivo === tab.props.id ? "tab-activo" : "")}
                                        href="#"
                                        key={tab.props.id}
                                        onClick={e => cambiarTab(e)}
                                    >
                                        {tab.props.id}
                                    </a>
                                );
                            }
                            return null;
                        })
                    }
                </div>
                <div className="btn-cerrar-semestre d-grid">
                    <Button variant="danger">Cerrar semestre</Button>{' '}
                </div>
            </nav>
            {
                children.map((contenidoTab) => {
                    if (isValidElement(contenidoTab) && contenidoTab.props.id === tabActivo) {
                        return (
                            <div key={contenidoTab.props.id} className="tabs-content">
                                {contenidoTab}
                            </div>
                        );
                    }
                    return null;
                })
            }
        </div>
    )
}

export default Tabs;