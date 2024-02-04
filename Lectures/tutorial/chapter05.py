from datetime import date
from enum import Enum
from typing import Optional, List

from fastapi import APIRouter, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Field

app05 = APIRouter()