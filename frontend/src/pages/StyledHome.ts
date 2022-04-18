import { styled } from '@mui/system';
import { TextField, Button, Paper} from '@mui/material';

export const FormContainer = styled(Paper)`
    display: flex;
    flex-direction: column;
    box-shadow: 4px 6px 15px rgba(0, 0, 0, 0.2);
    border-radius: 1.2rem;
    margin-top: 6rem;
    padding: 4rem;
    justify-content: center;
    align-items: center;

    h1,h2,h3,h4,h5,h6 {
        color: inherit;
        margin-bottom: 2.5rem;
    }
`

export const StyledButton = styled(Button)`
    margin-top: 1.5em;
    margin-bottom: 3em;
    padding: 1rem;
`