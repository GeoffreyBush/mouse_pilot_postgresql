sequenceDiagram
    participant R as Researcher
    box 
    participant M as MousePilot GUI
    participant D as Database
    end
    participant B as Breeding Wing
    
    R->>+M: Request put in for mouse
    M-->>+D: Request validated & stored
    D-->>+M: Request visible on GUI
    M->>+B: *Need notification system*
    B<<->>R: Messages regarding the active request can be exchanged using MousePilot or email
    B-->>+B: Requested task on mouse performed
    B->>+M: Request updated as complete
    M-->>+D: Request recorded as completed
    M-->>+D: Updated mouse details recorded (e.g. genotyped, culled)
    D-->>+M: Updated mouse details visible on GUI
    M->>+R: *Need notification system*