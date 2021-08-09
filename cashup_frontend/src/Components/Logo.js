import React from 'react';
import styled from 'styled-components';

const SLogo = styled.div`
    position: relative;
`;

function Logo() {
    return(
        <SLogo>
            <svg xmlns="http://www.w3.org/2000/svg" xlink="http://www.w3.org/1999/xlink" width="150" height="70" viewBox="0 0 200 126">
            <defs>
                <filter id="사각형_1" x="20" y="36" width="85" height="86" filterUnits="userSpaceOnUse">
                <feOffset dy="3" input="SourceAlpha"/>
                <feGaussianBlur stdDeviation="3" result="blur"/>
                <feFlood flood-opacity="0.161"/>
                <feComposite operator="in" in2="blur"/>
                <feComposite in="SourceGraphic"/>
                </filter>
                <filter id="사각형_2" x="38" y="20" width="85" height="86" filterUnits="userSpaceOnUse">
                <feOffset dy="3" input="SourceAlpha"/>
                <feGaussianBlur stdDeviation="3" result="blur-2"/>
                <feFlood flood-opacity="0.161"/>
                <feComposite operator="in" in2="blur-2"/>
                <feComposite in="SourceGraphic"/>
                </filter>
                <filter id="사각형_3" x="58" y="7" width="85" height="86" filterUnits="userSpaceOnUse">
                <feOffset dy="3" input="SourceAlpha"/>
                <feGaussianBlur stdDeviation="3" result="blur-3"/>
                <feFlood flood-opacity="0.161"/>
                <feComposite operator="in" in2="blur-3"/>
                <feComposite in="SourceGraphic"/>
                </filter>
                <clipPath id="clip-맞춤형_크기_1">
                <rect width="200" height="126"/>
                </clipPath>
            </defs>
            <g id="맞춤형_크기_1" data-name="맞춤형 크기 – 1" clip-path="url(#clip-맞춤형_크기_1)">
                <rect width="200" height="126" fill="#fff"/>
                <g transform="matrix(1, 0, 0, 1, 0, 0)" filter="url(#사각형_1)">
                <g id="사각형_1-2" data-name="사각형 1" transform="translate(34 47)" fill="#fff" stroke="#db9fb4" stroke-linejoin="round" stroke-width="5">
                    <rect width="57" height="58" stroke="none"/>
                    <rect x="-2.5" y="-2.5" width="62" height="63" fill="none"/>
                </g>
                </g>
                <g transform="matrix(1, 0, 0, 1, 0, 0)" filter="url(#사각형_2)">
                <g id="사각형_2-2" data-name="사각형 2" transform="translate(52 31)" fill="rgba(255,255,255,0.24)" stroke="#7bdee6" stroke-linejoin="round" stroke-width="5">
                    <rect width="57" height="58" stroke="none"/>
                    <rect x="-2.5" y="-2.5" width="62" height="63" fill="none"/>
                </g>
                </g>
                <g transform="matrix(1, 0, 0, 1, 0, 0)" filter="url(#사각형_3)">
                <g id="사각형_3-2" data-name="사각형 3" transform="translate(72 18)" fill="rgba(255,255,255,0.24)" stroke="#d1ef90" stroke-linejoin="round" stroke-width="5">
                    <rect width="57" height="58" stroke="none"/>
                    <rect x="-2.5" y="-2.5" width="62" height="63" fill="none"/>
                </g>
                </g>
                <text id="CashUp" transform="translate(34 49)" fill="#707070" font-size="40" font-family="BMJUAOTF, BM JUA_OTF"><tspan x="0" y="32">CashUp</tspan></text>
            </g>
            </svg>
        </SLogo>
    );
}

export default Logo;