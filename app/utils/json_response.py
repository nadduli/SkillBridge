#!/usr/bin/python3

"""JSON response utilities"""

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from json import dumps
from typing import Any, Dict, List, Optional


class JSONResponseDict(JSONResponse):
    """JSON response with dictionary data"""

    def __init__(
        self,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        error: str = "",
        status_code: int = 200,
    ):
        """Initialize your json response"""

        self.message = message
        self.data = data
        self.error = error
        self.status_code = status_code

        super().__init__(
            content=jsonable_encoder(self.response()), status_code=status_code
        )

    def __repr__(self):
        """Return a string representation of the JSON response"""
        return str({
            "message": self.message,
            "data": self.data,
            "error": self.error,
            "status_code": self.status_code,
        })

    def __str__(self):
        """Return a string representation of the JSON response"""
        return dumps({
            "message": self.message,
            "data": self.data,
            "error": self.error,
            "status_code": self.status_code,
        })

    def response(self):
        """Return the response data"""
        if self.status_code < 300:
            return {
                "message": self.message,
                "data": self.data,
                "status_code": self.status_code,
            }
        else:
            return {
                "message": self.message,
                "error": self.error,
                "status_code": self.status_code,
            }
