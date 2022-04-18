import { StyledBackground } from "./StyledBackground";
const Background = ({children}) => {
    return (
        <StyledBackground>
            {children}
        </StyledBackground>
    )
}
export default Background;