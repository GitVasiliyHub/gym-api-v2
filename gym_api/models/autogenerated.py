from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='user_pkey'),
        UniqueConstraint('email', name='user_email_key'),
        UniqueConstraint('phone', name='user_phone_key'),
        UniqueConstraint('username', name='user_username_key'),
        {'schema': 'gym'}
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(Text)
    phone: Mapped[str] = mapped_column(Text)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[Optional[str]] = mapped_column(Text)
    last_name: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)

    gymer: Mapped[List['Gymer']] = relationship('Gymer', back_populates='user')
    master: Mapped[List['Master']] = relationship('Master', back_populates='user')


class Gymer(Base):
    __tablename__ = 'gymer'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['gym.user.user_id'], name='gymer_user_id_fkey'),
        PrimaryKeyConstraint('gymer_id', name='gymer_pkey'),
        {'schema': 'gym'}
    )

    gymer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user: Mapped[Optional['User']] = relationship('User', back_populates='gymer')
    task_group: Mapped[List['TaskGroup']] = relationship('TaskGroup', back_populates='gymer')


class Master(Base):
    __tablename__ = 'master'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['gym.user.user_id'], name='master_user_id_fkey'),
        PrimaryKeyConstraint('master_id', name='master_pkey'),
        {'schema': 'gym'}
    )

    master_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    user: Mapped[Optional['User']] = relationship('User', back_populates='master')
    exercise: Mapped[List['Exercise']] = relationship('Exercise', back_populates='master')
    task_group: Mapped[List['TaskGroup']] = relationship('TaskGroup', back_populates='master')


class Exercise(Base):
    __tablename__ = 'exercise'
    __table_args__ = (
        ForeignKeyConstraint(['master_id'], ['gym.master.master_id'], name='exercise_master_id_fkey'),
        PrimaryKeyConstraint('exercise_id', name='exercise_pkey'),
        {'schema': 'gym'}
    )

    exercise_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    master_id: Mapped[Optional[int]] = mapped_column(Integer)

    master: Mapped[Optional['Master']] = relationship('Master', back_populates='exercise')
    exercise_desc: Mapped[List['ExerciseDesc']] = relationship('ExerciseDesc', back_populates='exercise')


class MasterGym(Base):
    __tablename__= 'master_gym'
    __table_args__ = (
        PrimaryKeyConstraint('master_id', 'gymer_id', 'create_dttm'),
        ForeignKeyConstraint(['gymer_id'], ['gym.gymer.gymer_id'], name='master_gym_gymer_id_fkey'),
        ForeignKeyConstraint(['master_id'], ['gym.master.master_id'], name='master_gym_master_id_fkey'),    
        {'schema': 'gym'}
    )
    master_id: Mapped[int] = mapped_column(Integer)
    gymer_id: Mapped[Optional[int]] = mapped_column(Integer)
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    close_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))



class TaskGroup(Base):
    __tablename__ = 'task_group'
    __table_args__ = (
        ForeignKeyConstraint(['gymer_id'], ['gym.gymer.gymer_id'], name='task_group_gymer_id_fkey'),
        ForeignKeyConstraint(['master_id'], ['gym.master.master_id'], name='task_group_master_id_fkey'),
        PrimaryKeyConstraint('task_group_id', name='task_group_pkey'),
        {'schema': 'gym'}
    )

    task_group_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(15), server_default=text("'planed'::character varying"))
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    master_id: Mapped[Optional[int]] = mapped_column(Integer)
    gymer_id: Mapped[Optional[int]] = mapped_column(Integer)
    properties: Mapped[Optional[dict]] = mapped_column(JSONB)
    update_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    gymer: Mapped[Optional['Gymer']] = relationship('Gymer', back_populates='task_group')
    master: Mapped[Optional['Master']] = relationship('Master', back_populates='task_group')
    task: Mapped[List['Task']] = relationship('Task', back_populates='task_group')


class ExerciseDesc(Base):
    __tablename__ = 'exercise_desc'
    __table_args__ = (
        ForeignKeyConstraint(['exercise_id'], ['gym.exercise.exercise_id'], name='exercise_desc_exercise_id_fkey'),
        PrimaryKeyConstraint('exercise_desc_id', name='exercise_desc_pkey'),
        {'schema': 'gym'}
    )

    exercise_desc_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    exercise_id: Mapped[Optional[int]] = mapped_column(Integer)

    exercise: Mapped[Optional['Exercise']] = relationship('Exercise', back_populates='exercise_desc')
    task: Mapped[List['Task']] = relationship('Task', back_populates='exercise_desc')


class Task(Base):
    __tablename__ = 'task'
    __table_args__ = (
        ForeignKeyConstraint(['exercise_desc_id'], ['gym.exercise_desc.exercise_desc_id'], name='task_exercise_desc_id_fkey'),
        ForeignKeyConstraint(['task_group_id'], ['gym.task_group.task_group_id'], name='task_task_group_id_fkey'),
        PrimaryKeyConstraint('task_id', name='task_pkey'),
        {'schema': 'gym'}
    )

    task_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(15), server_default=text("'planed'::character varying"))
    create_dttm: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=text('now()'))
    task_group_id: Mapped[Optional[int]] = mapped_column(Integer)
    exercise_desc_id: Mapped[Optional[int]] = mapped_column(Integer)
    properties: Mapped[Optional[dict]] = mapped_column(JSONB)
    update_dttm: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    exercise_desc: Mapped[Optional['ExerciseDesc']] = relationship('ExerciseDesc', back_populates='task')
    task_group: Mapped[Optional['TaskGroup']] = relationship('TaskGroup', back_populates='task')
