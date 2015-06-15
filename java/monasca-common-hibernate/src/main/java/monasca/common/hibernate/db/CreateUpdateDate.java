/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package monasca.common.hibernate.db;

import javax.persistence.Column;
import javax.persistence.MappedSuperclass;

import org.hibernate.annotations.Parameter;
import org.hibernate.annotations.Type;
import org.joda.time.DateTime;

@MappedSuperclass
public abstract class CreateUpdateDate {

  public CreateUpdateDate() {
    super();
  }

  public CreateUpdateDate(DateTime created_at, DateTime updated_at) {
    super();
    this.created_at = created_at;
    this.updated_at = updated_at;
  }

  @Column(name = "created_at")
  @Type(type = "org.jadira.usertype.dateandtime.joda.PersistentDateTime", parameters = {@Parameter(name = "databaseZone", value = "UTC"),
      @Parameter(name = "javaZone", value = "jvm")})
  private DateTime created_at;

  @Column(name = "updated_at")
  @Type(type = "org.jadira.usertype.dateandtime.joda.PersistentDateTime", parameters = {@Parameter(name = "databaseZone", value = "UTC"),
      @Parameter(name = "javaZone", value = "jvm")})
  private DateTime updated_at;

  public DateTime getCreated_at() {
    return created_at;
  }

  public void setCreated_at(DateTime created_at) {
    this.created_at = created_at;
  }

  public DateTime getUpdated_at() {
    return updated_at;
  }

  public void setUpdated_at(DateTime updated_at) {
    this.updated_at = updated_at;
  }
}
