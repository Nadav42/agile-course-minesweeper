import React from 'react';
import { toast } from 'react-toastify';

import socketIOClient from "socket.io-client";

import { socket_host, getLobbiesList, postJoinLobby, postJoinLobbyWithPassword, postCreateLobby } from '../../api/rest_api'

function LobbiesTable(props) {
    let lobbies = props.lobbies;

    if (!lobbies || !lobbies.length) {
        return "Loading lobby list...";
    }

    let lobbiesElements = lobbies.map(lobby => {
        if (lobby.hasPassword) {
            return (
                <tr key={lobby.key} className="lobby-closed">
                    <td className="text-left">
                        <span className="lobby-icon"><i className="fas fa-lock"></i></span>
                        <span>{lobby.name}</span>
                    </td>
                    <td className="text-right">
                        <span className="span-link" data-toggle="modal" data-target="#passwordModal" onClick={() => props.handleSelectPasswordLobby(lobby.key)}>Join</span>
                    </td>
                </tr>
            );
        }
        else {
            return (
                <tr key={lobby.key} className="lobby-open">
                    <td className="text-left">
                        <span className="lobby-icon"><i className="fas fa-door-open"></i></span>
                        <span>{lobby.name}</span>
                    </td>
                    <td className="text-right">
                        <span className="span-link" onClick={() => props.handleJoinLobby(lobby.key)}>Join</span>
                    </td>
                </tr>
            );
        }
    })

    return (
        <div className="lobbies-list">
            <table className="table border">
                <tbody>
                    {lobbiesElements}
                </tbody>
            </table>
        </div>
    );
}

function PasswordModal(props) {
    return (
        <div className="modal fade" id="passwordModal" tabIndex="-1" role="dialog">
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Lobby requires password</h5>
                        <button type="button" className="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
                    </div>
                    <div className="modal-body">
                        <div className="form-group text-left">
                            <label>Password</label>
                            <input type="password" className="form-control" value={props.password} onChange={props.handlePasswordChange} />
                        </div>
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-primary" onClick={props.handleJoinLobbyWithPassword} data-dismiss="modal">Join</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

class LobbiesPanel extends React.Component {
    state = { lobbies: [], lobbyName: "", lobbyPassword: "", modalPassword: "", passwordModalLobbyKey: null }

    constructor(props) {
        super(props);

        this.socket = socketIOClient(socket_host);
    }

    componentDidMount() {
        this.updateLobbies();

        this.socket.on("lobbiesChanged", this.updateLobbies);
    }

    componentWillUnmount() {
        this.socket.off("lobbiesChanged", this.updateLobbies);
    }

    updateLobbies = async () => {
        let lobbies = await getLobbiesList();
        this.setState({ lobbies: lobbies });
    }

    handleJoinLobby = (lobbyKey) => {
        postJoinLobby(lobbyKey, () => {
            this.props.history.push("/game");
        });
    }

    handleJoinLobbyWithPassword = () => {
        let lobbyKey = this.state.passwordModalLobbyKey;
        let password = this.state.modalPassword;

        if (!lobbyKey) {
            return;
        }

        postJoinLobbyWithPassword(lobbyKey, password, () => {
            this.props.history.push("/game");
        });
    }

    handleCreateLobby = () => {
        postCreateLobby(this.state.lobbyName, this.state.lobbyPassword, () => {
            toast.success(`Created Lobby "${this.state.lobbyName}"`, {autoClose: 2750});
            this.props.history.push("/game");
        });
    }

    handleSelectPasswordLobby = (lobbyKey) => {
        this.setState({ modalPassword: "", passwordModalLobbyKey: lobbyKey });
    }

    handleModalPasswordChange = (e) => {
        this.setState({ modalPassword: e.target.value });
    }

    handleLobbyNameChange = (e) => {
        this.setState({ lobbyName: e.target.value });
    }

    handleLobbyCreatePasswordChange = (e) => {
        this.setState({ lobbyPassword: e.target.value });
    }

    render() {
        return (
            <div className="pt-1">
                <LobbiesTable lobbies={this.state.lobbies} handleJoinLobby={this.handleJoinLobby} handleSelectPasswordLobby={this.handleSelectPasswordLobby} />

                <div className="mb-4"></div>
                <hr></hr>
                <div className="mx-auto lobby-form text-left">
                    <div className="form-group">
                        <label>Lobby Name</label>
                        <input type="text" className="form-control" value={this.state.lobbyName} onChange={this.handleLobbyNameChange} />
                    </div>
                    <div className="form-group">
                        <label>Lobby Password</label>
                        <input type="password" className="form-control" placeholder="Optional (leave empty)" value={this.state.lobbyPassword} onChange={this.handleLobbyCreatePasswordChange} />
                    </div>
                    <div className="text-center">
                        <button type="button" className="btn btn-success" onClick={this.handleCreateLobby}>Create Lobby</button>
                    </div>
                </div>

                <PasswordModal password={this.state.modalPassword} handlePasswordChange={this.handleModalPasswordChange} handleJoinLobbyWithPassword={this.handleJoinLobbyWithPassword} />
            </div>
        );
    }
}

export default LobbiesPanel;
