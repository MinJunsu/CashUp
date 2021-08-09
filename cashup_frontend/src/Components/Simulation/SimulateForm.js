import React from 'react';
import styled from 'styled-components';
import { useForm } from 'react-hook-form';

const Container = styled.div`
`;

const Form = styled.form`
    display: flexbox;
    padding-top: 10px;
`;

const DateField = styled.input`
    margin-bottom: 10px;
    display: inline-flex;
    margin-right: 10px;
    margin-left: 10px;
    border: 1px;
    border-color: inherit;
`;

const InputField = styled.input`
    width: 50px;
    margin-left: 10px;
    margin-right: 10px;
    box-sizing: inherit;
    display: inline-flex;
`;

const Label = styled.label`
    display: inline-flex;
`;

const RadioField = styled.div`
    text-align: center;
    display: inline;
	overflow: hidden;
`;

const RadioLabel = styled.label`
    height: 20px;
	color: rgba(0, 0, 0, 0.6);
	line-height: 1;
	text-align: center;
	padding: 8px 16px;
	margin-right: -1px;
	border: 1px solid rgba(0, 0, 0, 0.2);
	box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3), 0 1px rgba(255, 255, 255, 0.1);
	transition: all 0.2s ease-in-out;
    :hover{
        cursor: pointer;
    }
    :first-of-type{
        border-radius: 4px 0 0 4px;
    }
    :last-of-type {
        border-radius: 0 4px 4px 0;
        margin-right: 5px;
    }
`;

const RadioButton = styled.input`
    height: 20px;
    position: absolute !important;
	clip: rect(0, 0, 0, 0);
	height: 1px;
	width: 1px;
	border: 0;
	overflow: hidden;
    :checked + ${RadioLabel}{
        background-color: #a5dc86;
	    box-shadow: none;
    }
`;



function SimulateForm(props) {
    const { register, handleSubmit } = useForm();
    const onSubmit = data => {
        props.setFormData(data);
        alert('실행');
    }
    return (
        <Container>
            <Form onSubmit={handleSubmit(onSubmit)}>
                <div className="form-row">
                    <Label htmlFor="startTime">시작일</Label>
                    <DateField type="date" defaultValue='2018-01-01' {...register('startTime')} className="form" id="startTime"/>
                    <Label htmlFor="endTime">종료일</Label>
                    <DateField type="date" defaultValue='2022-01-01' {...register('endTime')} className="form" id="endTime"/>
                    <Label htmlFor="buyRate">구매 호가</Label>
                    <InputField defaultValue='30' type="text" {...register('buyRate')} id="buyRate" placeholder="50"/>
                    <Label htmlFor="sellRate">판매 호가</Label>
                    <InputField defaultValue='50' type="text" {...register('sellRate')} id="sellRate" placeholder="30"/>
                    <RadioField>
                        <RadioButton type="radio" value='long' {...register('type')} id="longRadio" name='type'/>
                        <RadioLabel htmlFor="longRadio">공매수</RadioLabel>
                        <RadioButton type="radio" value='short' {...register('type')} id="shortRadio" name='type'/>
                        <RadioLabel htmlFor="shortRadio">공매도</RadioLabel>
                    </RadioField>
                    <RadioField>
                        <RadioButton type="radio" value='1' {...register('version')} id="version1" name='version'/>
                        <RadioLabel htmlFor="version1">Ver.1</RadioLabel>
                        <RadioButton type="radio" value='2' {...register('version')} id="version2" name='version'/>
                        <RadioLabel htmlFor="version2">Ver.2</RadioLabel>
                        <RadioButton type="radio" value='3' {...register('version')} id="version3" name='version'/>
                        <RadioLabel htmlFor="version3">Ver.3</RadioLabel>
                    </RadioField>
                    <button type="submit">시뮬레이션</button>
                </div>
            </Form>
        </Container>
    );
}

export default SimulateForm;


